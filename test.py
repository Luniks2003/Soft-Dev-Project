ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'html', 'pdf'}

file = "hello.txt"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

print(allowed_file(file))