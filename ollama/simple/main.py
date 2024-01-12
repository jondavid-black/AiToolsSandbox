from langchain.llms import Ollama

# input = input("What is your question? ")
input = "Provide a Python function that accepts numbers a, b, and c for and computes the formula $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$."
llm = Ollama(model="codebot")
res = llm.predict(input)
print (f"Answer: {res}")
