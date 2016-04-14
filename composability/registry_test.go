package composability

import (
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

func TestLoadTemplate(t *testing.T) {
	wd, err := os.Getwd()
	if err != nil {
		t.Error("TestLoadTemplate: os.Getwd() failed")
	}
	r := NewRegistry(filepath.Dir(wd))
	def := r.LoadTemplate("patient.json")
	fmt.Println(def.Name)
}
