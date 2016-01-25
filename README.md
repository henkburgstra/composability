#Composability
Composable views for python - work in progress

##View ABC
Interface voor concrete View implementaties

##View implementatie
Concrete implementatie, bijvoorbeeld wx of qt
X - template X dit is niet een attribuut. Bij het laden vraagt de view een
  pad aan de controller, die geeft een gevulde template terug.
- controller

##Binder
- Binds data to the template
- Binder.Load(template)
- Binder.LoadRelationship(template, relationship)
- Binder.Bind(template, data)

##Template
Verzameling GUI-elementen, ingelezen uit JSON-definities
- kind: enkelvoudig (TEXT, LABEL, ...) of CONTAINER
- elements: array kinderen
- orientation: HORIZONTAL, VERTICAL
- display: INLINE, RIGHT, ..

##Controller
Controls the view
Controller(View, Binder)



