with open("input_blocks.txt") as file:
	content = file.read()
for idx, block in enumerate(content.strip().split("---\n")):
	with open(f"blocks/{idx+1}.txt", "w") as file:
		print(block.rstrip(), file=file)