package composability

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"path"
)

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

func (r *Registry) LoadDefItem(def *Template) *Template {
	return def
}

func ReadError(filename string) {
	panic(fmt.Sprintf("Can't open template %s", filename))
}
func (r *Registry) LoadTemplate(name string) *Template {
	filename := path.Join(r.defPath, name)
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		ReadError(filename)
	}
	var t Template
	err = json.Unmarshal(data, &t)
	if err != nil {
		panic(fmt.Sprintf("Can't unmarshal %s: %s", filename, err.Error()))
	}
	return r.LoadDefItem(&t)
}
