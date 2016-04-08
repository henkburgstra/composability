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

func (r *Registry) IncludeDef(parent *Template) *Template {
	return nil
}

func (r *Registry) ExtendDef(parent *Template) *Template {
	return nil
}

func (r *Registry) LoadDef(def *Template) *Template {
	extended := r.ExtendDef(def)
	if extended != nil {
		return extended
	}
	include := r.IncludeDef(def)
	var template *Template
	if include == nil {
		template = NewTemplate(def.Kind)
		template.Name = def.Name
		template.Title = def.Title
		template.Readonly = def.Readonly
		template.Visible = def.Visible
		for _, item := range def.Items {
			template.Add(item)
		}
	} else {
		template = include
		template.Name = def.Name
		template.Title = def.Title
	}

	for key, value := range def.Attributes {
		template.Attributes[key] = value
	}

	return template
}

func (r *Registry) LoadTemplate(name string) *Template {
	filename := path.Join(r.defPath, name)
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(fmt.Sprintf("Can't open template %s", filename))
	}
	t := NewTemplate("container")
	err = json.Unmarshal(data, t)
	if err != nil {
		panic(fmt.Sprintf("Can't unmarshal %s: %s", filename, err.Error()))
	}
	return r.LoadDef(t)
}
