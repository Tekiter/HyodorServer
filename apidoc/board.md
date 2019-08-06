**게시판 목록**
----
게시판의 목록을 봅니다.

* **URL**

  /api/v1/board

* **Method:**
  
  `GET`

* **인자**

  None

* **성공 응답:**

  * **Code:** 200 OK
  * **Content:** 
```javascript
{
    "boards":[
        {
            "id": 1,
            "name": "testboard",
            "count": 37
        },
        {
            "id": 2,
            "name": "board2",
            "count": 2
        }
    ]
}
```
 
* **에러 응답:**

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

* **Sample Call:**

    None

* **Notes:**

    None



**게시판 생성**
----
게시판을 새로 생성합니다.

* **URL**

  /api/v1/board

* **Method:**
  
  `POST`

* **인자**

  **필수:**
 
   `name=[string]` : 게시판 이름 <br />

* **헤더**

  `Authorization: Bearer <JWT access 토큰>` 필요

* **성공 응답:**

  * **Code:** 200
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 로그인 토큰이 없을 때

  OR

  * **Code:** 403 Forbidden
  * **Description:** 유저의 권한이 부족할 때

  OR

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

* **Sample Call:**

    None

* **Notes:**

    로그인된 권한이 일정 권한 이상일때만 동작한다.


**게시글 목록**
----
게시글의 목록을 봅니다.

* **URL**

  /api/v1/board/<int:board_id>

* **Method:**
  
  `GET`

* **인자**

  **옵션:**
 
   `page=[int]` : 목록의 페이지 <br />
   `pagesize=[int]` : 페이지당 게시글 수 <br />

* **성공 응답:**

  * **Code:** 200
  * **Content:** 
```javascript
{
    "totalcount": 37,
    "count": 10,
    "posts":[
        {"id": 42, "title": "title1", "content": "content1", "vote_up": 0,…},
        {"id": 41, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 40, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 39, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 38, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 37, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 36, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 35, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 34, "title": "title2", "content": "content2", "vote_up": 0,…},
        {"id": 33, "title": "title2", "content": "content2", "vote_up": 0,…}
    ]
}
```
 
* **에러 응답:**

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

  OR

  * **Code:** 404 NOT FOUND
  * **Description:** 해당하는 게시판이 없을 때

* **Sample Call:**

    None

* **Notes:**

    None


**게시글 작성**
----
게시글을 씁니다.

* **URL**

  /api/v1/board/<int:board_id>

* **Method:**
  
  `POST`

* **인자**

  **필수:**
 
   `title=[int]` : 제목 <br />
   `content=[int]` : 내용 <br />

* **성공 응답:**

  * **Code:** 200
  * **Content:** ```{}```
 
* **에러 응답:**

  * **Code:** 401 UNAUTHORIZED
  * **Description:** 로그인 토큰이 없을 때

  OR

  * **Code:** 400 BAD REQUEST
  * **Description:** 올바른 매개변수가 아닐 때

  OR

  * **Code:** 403 Forbidden
  * **Description:** 유저의 권한이 부족할 때

* **Sample Call:**

    None

* **Notes:**

    None