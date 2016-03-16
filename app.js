var bezoek = {
  "kind": "CONTAINER",
  "name": "bezoek",
  "title": "bezoek {key}",
  "attributes": {
    "orientation": "HORIZONTAL",
    "display": "INLINE",
    "background_colour": "#e6e5a8",
    "colcount": 2,
    "label_position": "LEFT"
  },
  "items": [
    {
      "kind": "DATE",
      "name": "datum",
      "title": "Datum"
    },
    {
      "kind": "CONTAINER",
      "title": "Verrichtingen",
      "attributes": {
        "display": "INLINE",
        "orientation": "HORIZONTAL",
        "background_colour": "#28A9E1",
        "colcount": 1
      },
      "items": [
        {
          "kind": "CONTAINER",
          "name": "verrichtingen",
          "attributes": {
            "display": "INLINE",
            "orientation": "HORIZONTAL",
            "colcount": 1
          },
          "items": [
            {
              "kind": "TEXT",
              "name": "verrichting",
              "attributes": {
                "readonly": true
              }
            }
          ]
        },
        {
          "kind": "COMBO",
          "name": "verrichting_selectie",
          "attributes": {
            "placeholder": "Selecteer een verrichting"
          }
        }
      ]
    }
  ]
};

document.addEventListener('DOMContentLoaded', function() {
    var b = new BoxPanel(document.getElementById("composability-test"), "bezoek");
    var t = new Template();
    t.loadObject(bezoek);
    b.setTemplate(t);
    b.render();
});