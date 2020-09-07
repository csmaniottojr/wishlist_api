from src.customer import product_api


def test_exists_product_with_id_returns_true():
    assert (
        product_api.exists_product_with_id('1bf0f365-fbdd-4e21-9786-da459d78dd1f')
        is True
    )


def test_exists_product_with_id_returns_false():
    assert (
        product_api.exists_product_with_id('5ddbc2b9-1186-4c38-b65e-ce8949ee91b5')
        is False
    )
