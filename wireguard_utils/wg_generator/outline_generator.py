import requests

from pydantic import BaseModel, Field

from bot.data import config


class AccessKey(BaseModel):
    id: str
    access_url: str = Field(alias="accessUrl")


def generate_new_key(key_name: str) -> str:
    response = requests.post(f"{config.BASE_MANAGEMENT_URL}/access-keys", verify=False)

    response.raise_for_status()

    key = AccessKey.parse_obj(response.json())

    response = requests.put(
        f"{config.BASE_MANAGEMENT_URL}/access-keys/{key.id}/name",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"name": key_name},
        verify=False,
    )

    response.raise_for_status()

    return key.access_url


if __name__ == "__main__":
    generate_new_key("Русское имя с пробелами")
