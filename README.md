# integration-fox-coding

## gen.py

### Usage

```
$ python gen.py -h
usage: gen.py [-h] [--rows int] [--output_path save_path] --column column_data
              [column_data ...]

A script, that when executed from the command line can accept up to three
named options and output a csv file in a local directory of the server we
execute it from

optional arguments:
  -h, --help            show this help message and exit
  --rows int            will dictate the number of rows in the output csv file
                        (default: 50)
  --output_path save_path
                        where the generated csv file will be saved new
                        directories will not be created and write permissions
                        must already be in place (default: current directory)
  --column column_data [column_data ...]
                        form of the argument must be: column_name,type where
                        type is either "integer" or "string" - MUST be
                        specified at least once but can be specified multiple
                        times


```

### Run locally
Create a virtual environment and activate it
```
$ python3 -m venv venv
$ . venv/bin/activate

```

### Test

Install pytest
```
$ pip install pytest

```
Run tests
```
$ pytest -v test_gen.py

```

## api.py

### Run with Docker
Build the image

```
$ docker build --tag fox .

```
Run in detached mode with port 5000 exposed

```
$ docker run -d -p 5000:5000 fox

```

### API

**Upload file**
----
 Push data to a file.

* **URL**

  /file

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
  None

* **Data Params**

  * `file=[file]`
  * `dzchunkindex=[integer]`
  * `dzchunkbyteoffset=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
  **Content:** `{ "Uploaded Chunk" }`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{ error : "File already exists" }`

  OR

  * **Code:** 500 <br />
    **Content:** `{ error : "Could not write the file to disk" }`

**Download file**
----
 Retrieve a file.

* **URL**

  /file/:filename

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
  `filename=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
  **Content:** `{ data: [File data] }`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{ error : "File does not exist" }`

### Run locally
Create a virtual environment and activate it
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install requirements.txt

```

### Test

Install pytest
```
$ pip install pytest

```
Create uploads folder
```
$ mkdir uploads

```
Run tests
```
$ pytest -v test_api.py

```