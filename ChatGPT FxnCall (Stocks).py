import yfinance as yf
import openai
import json

openai.api_key = open("Ready to upload\API Storage\OpenAI_API.txt", "r").read()

def get_current_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period="1mo").iloc[-1]) #You can add .Close or .Open to see just that
get_current_stock_price("C")

def run_conversation(user_message):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": user_message}]
    functions = [
        {
            "name": "get_current_stock_price", #name of the function
            "description": "Get the current stock price for a given symbol", #what this function does & its parameters
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                    },
                },
                "required": ["ticker"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(response_message)

    if response_message.get("function_call"):
        available_functions = {
            "get_current_stock_price": get_current_stock_price,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            ticker=function_args.get("ticker"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


print(run_conversation("Give me the current stock price of the company founded by Bill Gates"))

