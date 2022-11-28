def search(clen,val):
	bt = (val ^ 2511413510787461249559068661325070136171729934109381260690).to_bytes(24,"big")
	if len(set(bt)-set(range(127))) <= 0:
		print(bt)
		exit()
	if clen > 48:
		return
	for cur in range(16):
		ftr = 16 * val + cur
		if ftr % clen == 0:
			search(clen+1,ftr)
search(1,0)