import re
from exceptions.system.fatal_error import FatalError
from exceptions.validation_error import ValidationError
from werkzeug.exceptions import BadRequest


class ValidationMiddleware:
    VALIDATION_RULES_KEY = "validation"

    # Validator keys
    ERROR_MESSAGE = "message"
    VALIDATION_FUNCTION = "validator"

    # Validators
    IS_REQUIRED = "is_required"
    IS_NULLABLE = "is_nullable"
    REGEXP_PATTERN = "pattern"

    # Validation configuration
    FIELD_VALIDATORS = {
        IS_REQUIRED: {
            ERROR_MESSAGE: "Field '{field}' is required",
            VALIDATION_FUNCTION: lambda field_name, field_rules, data: field_name in data
        },
        IS_NULLABLE: {
            ERROR_MESSAGE: "Field '{field}' cannot be empty",
            VALIDATION_FUNCTION: lambda field_name, field_rules, data: (
                data.get(field_name) or field_rules.get(ValidationMiddleware.IS_NULLABLE, True)
            )
        },
        REGEXP_PATTERN: {
            ERROR_MESSAGE: "Field '{field}' does not match the pattern '{pattern}'",
            VALIDATION_FUNCTION: lambda field_name, field_rules, data: ValidationMiddleware._validate_regexp(
                field_name, field_rules, data
            )
        },
    }

    def __init__(self, router_rules):
        self.router_rules = {rule["rule"]: rule for rule in router_rules}

    def process_request(self, rule, request):
        """Main process method to validate the request."""
        route_config = self.router_rules.get(rule)
        if not route_config or ValidationMiddleware.VALIDATION_RULES_KEY not in route_config:
            return None  # No validation needed for this route

        validation_config = route_config[ValidationMiddleware.VALIDATION_RULES_KEY]

        # Check request content type
        if request.content_type.startswith("multipart/form-data"):
            self._validate_files(validation_config.get("fields", {}), request)
        else:
            self._validate_json(validation_config.get("fields", {}), request.json)

        return None  # No validation errors

    def _validate_json(self, fields, data):
        """Validate JSON fields."""
        for field_name, field_rules in fields.items():
            for validator_name, validator_config in self.FIELD_VALIDATORS.items():
                if validator_name in field_rules:
                    try:
                        is_valid = validator_config[ValidationMiddleware.VALIDATION_FUNCTION](
                            field_name, field_rules, data
                        )
                        if not is_valid:
                            raise self._create_error_response(validator_name, field_name, field_rules)
                    except KeyError as e:
                        raise ValidationError(message=f"Validation rule '{validator_name}' for field '{field_name}' requires missing key: '{e.args[0]}'.")

    def _validate_files(self, fields, request):
        """Validate file uploads."""
        for field_name, field_rules in fields.items():
            if field_name in request.files:
                file = request.files[field_name]
                # Validate file name with REGEXP_PATTERN
                if ValidationMiddleware.REGEXP_PATTERN in field_rules:
                    pattern = field_rules[ValidationMiddleware.REGEXP_PATTERN]
                    if not re.match(pattern, file.filename):
                        raise BadRequest(f"Invalid file format for '{field_name}'.")
            elif field_rules.get(ValidationMiddleware.IS_REQUIRED, False):
                # If the file is required but not provided
                raise BadRequest(f"Field '{field_name}' is required but missing.")

    def _create_error_response(self, validator_name, field_name, field_rules):
        """Generate an error response based on the validation failure."""
        validator_config = self.FIELD_VALIDATORS[validator_name]
        try:
            message = validator_config[self.ERROR_MESSAGE].format(
                field=field_name, **field_rules
            )
        except KeyError as e:
            missing_key = e.args[0]
            message = (
                f"Validation failed for field '{field_name}': Missing key '{missing_key}' "
                f"in field rules."
            )
        
        if message:
            raise ValidationError(user_notification=message)

        raise FatalError()

    @staticmethod
    def _validate_regexp(field_name, field_rules, data):
        """Check if the field matches the regexp."""
        value = data.get(field_name)
        pattern = field_rules.get(ValidationMiddleware.REGEXP_PATTERN)

        # If no pattern is provided, skip the validation
        if not pattern:
            return True

        try:
            # Compile the pattern to validate its correctness
            compiled_pattern = re.compile(pattern)
        except re.error:
            # Raise an error for invalid patterns
            raise ValidationError(
                user_notification="The provided data is wrong. Try again.",
                message=f"Invalid regexp pattern for field '{field_name}': {pattern}"
            )

        # Match the pattern against the value
        return bool(compiled_pattern.fullmatch(str(value)))
