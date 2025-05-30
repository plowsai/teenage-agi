
### Example copied from BabyAGI (https://babyagi.org/#function-metadata)

import teenagi 

@teenagi.register_function()
def world():
    return "world"

@teenagi.register_function(dependencies=["world"])
def hello_world():
    x = world()
    return f"Hello {x}!"

print(teenagi.hello_world())
if __name__ == "__main__":
    app = teenagi.create_app('/dashboard')
    app.run(host='0.0.0.0', port=8080)
