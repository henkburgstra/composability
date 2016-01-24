#Composability
Composable views for python - work in progress

##View ABC
Interface voor concrete View implementaties

##View implementatie
Concrete implementatie, bijvoorbeeld wx of qt
- template
- controller

##Template
Verzameling GUI-elementen, ingelezen uit JSON-definities
- kind: enkelvoudig (TEXT, LABEL, ...) of CONTAINER
- elements: array kinderen
- orientation: HORIZONTAL, VERTICAL
- display: INLINE, RIGHT, ..

