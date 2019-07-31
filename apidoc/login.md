**로그인**
----
사이트에 로그인합니다.

* **URL**

  /api/v1/login

* **Method:**
  
  `POST`

* **인자**

  **필수:**
 
   `username=[string]` : 유저의 아이디 <br />
   `password=[string]` : 유저의 비밀번호

* **성공 응답:**

  * **Code:** 200
  * **Content:** `{ username: "guest", "access_token": "[access token]", "refresh_token": "[refresh token]" }`
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 아이디 또는 비밀번호가 일치하지 않을 때
  * **Content:** `{ msg: "올바르지 않은 아이디 또는 비밀번호입니다." }`

  OR

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

* **Sample Call:**

    None

* **Notes:**

    None


**로그인 갱신**
----
refresh-token 으로 access-token 을 다시 발급 받습니다.

* **URL**

  /api/v1/login-refresh

* **Method:**
  
  `GET`

* **인자**

  None
* **헤더**

  `Authorization: Bearer <JWT refresh 토큰>` 필요

* **성공 응답:**

  * **Code:** 200
  * **Content:** `{ "access_token": "[access token]"}`
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** refresh token 도 만료되었을때 또는 헤더에 토큰이 없을 때

  OR

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

* **Sample Call:**

    None

* **Notes:**

    None


**회원가입**
----
회원가입을 합니다.

* **URL**

  /api/v1/register

* **Method:**
  
  `PUT`

* **인자**

  **필수:**
 
   `username=[string]` : 유저의 아이디 (중복불가) <br />
   `password=[string]` : 유저의 비밀번호 <br />
   `nickname=[string]` : 유저의 닉네임 <br />
   `email=[string]` : 유저의 이메일 (중복 불가)<br />

* **성공 응답:**

  * **Code:** 201 CREATED
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 아이디 또는 비밀번호가 일치하지 않을 때
  * **Content:** `{ msg: "올바르지 않은 아이디 또는 비밀번호입니다." }`

  OR

  * **Code:** 400 BAD REQUEST
  * **Description** 올바른 매개변수가 아닐 때 (아이디, 이메일 중복도 포함)

* **Sample Call:**

    None

* **Notes:**

    None

