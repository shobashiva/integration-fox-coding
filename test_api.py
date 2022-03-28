from api import create_app
import pytest
import io


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_hello(client):
    response = client.get('/')
    assert response.data == b'hello'


def test_get_file_dne(client):
    response = client.get('/file/fname.txt')
    assert response.data == b'File does not exist'
    assert response.status_code == 400


def test_post_file(client):
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    data['dzchunkindex'] = 1
    data['dzchunkbyteoffset'] = 1
    response = client.post(
        '/file',
        data=data
    )
    assert response.status_code == 200


def test_post_file_twice(client):
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    data['dzchunkindex'] = 0
    response = client.post(
        '/file',
        data=data
    )
    assert response.status_code == 400


def test_post_file_bad_path(client):  
    ''' bad paths are handled with secure_filename '''
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), '/dne/test.jpg')
    data['dzchunkindex'] = 1
    data['dzchunkbyteoffset'] = 1
    response = client.post(
        '/file',
        data=data
    )
    assert response.status_code == 200


def test_post_file_chunks(client):
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), 'test1.txt')
    data['dzchunkindex'] = 0
    data['dzchunkbyteoffset'] = 0
    response = client.post(
        '/file',
        data=data
    )
    assert response.status_code == 200

    data = {}
    data['file'] = (io.BytesIO(b"ghijkl"), 'test1.txt')
    data['dzchunkindex'] = 1
    data['dzchunkbyteoffset'] = 6
    response = client.post(
        '/file',
        data=data
    )
    assert response.status_code == 200


def test_get_file_chunk_in_order(client):
    response = client.get('/file/test1.txt')
    assert response.status_code == 200
    assert response.data == b"abcdefghijkl"