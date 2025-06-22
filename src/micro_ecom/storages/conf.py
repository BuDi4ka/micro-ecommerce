from micro_ecom.env import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)

AWS_STORAGE_BUCKET_NAME = "micro-ecommerce-bucket"
AWS_S3_ENDPOINT_URL = "https://lon1.digitaloceanspaces.com"  # region-only endpoint
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_USE_SSL = True
AWS_DEFAULT_ACL = "public-read"  # Optional, depends on if your space is public

# Use custom storage backends
DEFAULT_FILE_STORAGE = "micro_ecom.storages.backends.MediaStorage"
STATICFILES_STORAGE = "micro_ecom.storages.backends.StaticFileStorage"
