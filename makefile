install:
	 pip3 install -r requirements.txt
run:
	 PYTHONPATH=../.. python3 -m main
eval:
	 PYTHONPATH=evals python3 -m function_evals