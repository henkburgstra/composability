package composability

type Registry struct {
	defPath   string
	templates map[string]*Template
}

func NewRegistry(defPath string) *Registry {
	r := new(Registry)
	r.defPath = defPath
	r.templates = make(map[string]*Template)
	return r
}
