if last2col[0] != "g":
 	probabilitySameCol = (chances[0] / 15) ** lastam
 	print(str(probabilitySameCol))
 probabilityGreen = 1 - ((15 - chances[2]) / 15)
 probabilityOtherCol = 1 - probabilityGreen - probabilitySameCol