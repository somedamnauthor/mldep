import transformers
#print(torch.__version__)
def main(args):
	print("Inside test1 function")
	return {"Transformers version": transformers.__version__}
