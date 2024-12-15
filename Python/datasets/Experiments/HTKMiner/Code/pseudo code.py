function UpdateTopK(List1, minSupportThreshold){
	nextLevelList = {}
	while (len(list1)):
			key, element = getElement(list, i)
		while (len(list1)):
			key1, element1 = getElement(list, j)
			prefix1= getPrex(elment)
			prefix2= getPrex(elment1)
			if(prefix1 == prefix2)
				 newElement = joinElement(elment, elment1)
			
			minSupport = getSupportThreshold(newElement)
			
			if(minSupport >= minSupportThreshold) {
				putElementInTopKList(newElement)
				InsertElementIn(nextLevelList, newElement)
			}	
			
	UpdateTopK(nextLevelList)
}
------------------------
List1 = {
			[0] => [AB] // element
				   [6]  // support 
			[1] => [AC] // element
				   [4]  // support
			.....
			.....	
		}
Next level Would be
List1 = {
			[0] => [ABC] // element
				   [4]  // support 
			.....
			.....	
		}			
		