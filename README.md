### Checking connection frontend and backend

- Clone the branch connect_checking
- Launch the docker container
- Send a request to the localhost:8888/checking
- request must be in the JSON fromat:
 ### example:
  {
    "code": "Hello"
  }
- the response is going to be in a JSON fromat and contains two fields "checking_status" and "hashed_code":
  ### example:
  {
    "checking_status": "successfully done",
    "hashed_code": "0d3e41ad6dd57b3a239c7751240712752550b95a381b1a7a3f67a86f91b62959"
  }
  
  
