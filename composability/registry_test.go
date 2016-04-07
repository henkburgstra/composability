package composability

import (
	"fmt"
	"testing"
)

func TestLoadTemplate(t *testing.T) {
	r := NewRegistry(`d:\projecten\python\composability`)
	def := r.LoadTemplate("patient.json")
	fmt.Println(def.Name)
}
