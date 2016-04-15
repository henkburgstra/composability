package composability

//interface ITransformer {
//	func Display() string;
//	func Store() string;
//}

type TransformerDisplay func() string
type TransformerStore func() string

type Transformer struct {
	Attributes map[string]*Attribute
	Display    TransformerDisplay
	Store      TransformerStore
}

func NewTransformer(kwargs map[string]*Attribute) *Transformer {
	t := new(Transformer)
	t.Attributes = kwargs
	t.Display = func() string {
		if v, ok := t.Attributes["value"]; ok {
			return v.String()
		} else {
			return ""
		}
	}
	t.Store = func() string {
		return t.Display()
	}
	return t
}
