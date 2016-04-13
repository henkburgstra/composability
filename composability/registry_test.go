package composability

import (
	"fmt"
	"os"
	"path"
	"testing"
)

func TestLoadTemplate(t *testing.T) {
	wd, err := os.Getwd()
	if err != nil {
		t.Error("TestLoadTemplate: os.Getwd() failes")
	}
	r := NewRegistry(path.Dir(wd))
	def := r.LoadTemplate("patient.json")
	fmt.Println(def.Name)
}
