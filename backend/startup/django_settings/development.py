from django.core.management.utils import get_random_secret_key

"""開発環境等.envが存在しない場合に使用"""


class StdIO():
    """ファイル操作クラス"""

    def __init__(self):
        self.path = r'/usr/src/app/.env'
        with open(self.path, mode='w'):
            pass

    def write(self, string):
        with open(self.path, mode='a') as f:
            f.write(string + '\n')


def generate_secret_key():
    return f'SECRET_KEY={get_random_secret_key()}'


def generate_allowed_hosts():
    return 'ALLOWED_HOSTS=*' + '\n'


def get_default_database_url():
    return r'DATABASE_URL=postgresql://testuser:password@localhost:5432/testdb'


def write_dummy_params(env_file):
    array = [
        'CORS_ORIGIN_WHITELIST=https://example.com',
        'AWS_ACCESS_KEY_ID=dummy',
        'AWS_SECRET_ACCESS_KEY=dummy',
        'AWS_STORAGE_BUCKET_NAME=dummy',
        'SITE_EMAIL=dummy',
        'EMAIL_PASSWORD_SUB=dummy',
        'EMAIL_PASSWORD=dummy',
        'GUEST_EMAIL=dummy',
        'GUEST_PASSWORD=dummy',
        'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=dummy',
        'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=dummy',
        'SOCIAL_AUTH_GITHUB_KEY=dummy',
        'SOCIAL_AUTH_GITHUB_SECRET=dummy',
        'SOCIAL_AUTH_GITHUB_KEY_LOCAL=dummy',
        'SOCIAL_AUTH_GITHUB_SECRET_LOCAL=dummy',
        'SOCIAL_AUTH_FACEBOOK_KEY=dummy',
        'SOCIAL_AUTH_FACEBOOK_SECRET=dummy',
        'SOCIAL_AUTH_FACEBOOK_KEY_LOCAL=dummy',
        'SOCIAL_AUTH_FACEBOOK_SECRET_LOCAL=dummy',
    ]

    [env_file.write(e) for e in array]


def main():
    env_file = StdIO()
    env_file.write(generate_secret_key())
    env_file.write(generate_allowed_hosts())
    env_file.write(get_default_database_url())
    write_dummy_params(env_file)


if __name__ == "__main__":
    main()
