[PHP]

; Maximum amount of memory a script may consume
; http://php.net/memory-limit
memory_limit = @{{ .Env.PHP_MEMORY_LIMIT }}

; Maximum allowed size for uploaded files.
; http://php.net/upload-max-filesize
upload_max_filesize = @{{ .Env.PHP_UPLOAD_MAX_FILESIZE }}

; Maximum size of POST data that PHP will accept.
; Its value may be 0 to disable the limit. It is ignored if POST data reading
; is disabled through enable_post_data_reading.
; http://php.net/post-max-size
post_max_size = @{{ .Env.PHP_POST_MAX_SIZE }}

{{-- OPCACHE --}}
@if ($prod)
[opcache]

; Determines if Zend OPCache is enabled
opcache.enable=1

; The OPcache shared memory storage size.
opcache.memory_consumption=512

; The amount of memory for interned strings in Mbytes.
opcache.interned_strings_buffer=64

; The maximum number of keys (scripts) in the OPcache hash table.
; Only numbers between 200 and 1000000 are allowed.
opcache.max_accelerated_files=30000

; When disabled, you must reset the OPcache manually or restart the
; webserver for changes to the filesystem to take effect.
opcache.validate_timestamps=0

; If disabled, all PHPDoc comments are dropped from the code to reduce the
; size of the optimized code.
opcache.save_comments=1
@endif
