**일정 목록**
----
로그인된 유저의 일정 목록을 조회합니다.

* **URL**

  /api/v1/schedule

* **Method:**
  
  `GET`

* **인자**

  None

* **성공 응답:**

  * **Code:** 200 OK
  * **Content:** 
```javascript
{  
   "schedules":[  
      {  
         "id":1,
         "type":1,
         "content":"일정",
         "datetime":"2019-08-12T14:50:59.256428"
      },
      {  
         "id":2,
         "type":1,
         "content":"으아아",
         "datetime":"2019-08-12T14:50:59.256428"
      }
   ]
}
```
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 로그인이 되어있지 않을 때

* **Sample Call:**

    None

* **Notes:**

    None



**일정 등록**
----
로그인된 유저의 일정을 등록합니다.

* **URL**

  /api/v1/schedule

* **Method:**
  
  `POST`

* **인자**

  **필수**

  `type=[int]` : 일정 타입 (클라이언트 단에서 맘대로 선택) <br />
  `content=[string]` : 일정 내용 <br />
  `datetime=[string]` : 날짜 (ISO 8601 형식으로 전송해야 함) <br />

* **성공 응답:**

  * **Code:** 201 CREATED
  * **Content:** ```{}```
 
* **에러 응답:**

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

  OR

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 로그인이 되어있지 않을 때

* **Sample Call:**

    None

* **Notes:**

    None



**일정 삭제**
----
로그인된 유저의 일정을 삭제합니다.

* **URL**

  /api/v1/schedule/`<int:schedule_id>`

* **Method:**
  
  `POST`

* **인자**

  **필수**

  None

* **성공 응답:**

  * **Code:** 200 SUCCESS
  * **Content:** ```{}```
 
* **에러 응답:**

  * **Code:** 404 NOT FOUND
  * **Description:** 일정이 존재하지 않을 때

  OR

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 로그인이 되어있지 않을 때

* **Sample Call:**

    None

* **Notes:**

    None
