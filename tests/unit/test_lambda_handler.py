from src.lambda_function_producer import handler


def test_lambda_handler_runs():
    response = handler({}, {})
    assert response["body"] == "Hello, world!"
    assert response["statusCode"] == 200
