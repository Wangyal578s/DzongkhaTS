from app import create_app

app = create_app()

if __name__ == "__main__":
    # host="0.0.0.0" allows access from any IP on your network
    # debug=True enables auto-reload and debug tools
    app.run(host="0.0.0.0", port=5050, debug=True)

