from capture import capture_screen
from uploader import upload


def main():

    image = capture_screen()

    result = upload(image)

    print(result)


if __name__ == "__main__":
    main()