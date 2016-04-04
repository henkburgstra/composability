package composability

type Template struct {
	Kind       string      `json:"kind"`
	Name       string      `json:"name"`
	Title      string      `json:"title"`
	Value      interface{} `json:"value"`
	Readonly   bool
	Visible    bool
	Items      []*Template
	items_map  map[string]*Template
	Attributes map[string]interface{} `json:"attributes"`
}

func NewTemplate(kind string) *Template {
	t := new(Template)
	t.Kind = kind
	t.Items = make([]*Template, 0, 0)
	t.items_map = make(map[string]*Template)
	return t
}
