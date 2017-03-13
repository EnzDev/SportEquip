$( function(){

  // Location autocomplete
  $("input.loc")[0].oninput = function(){
    var search = $(this).val()
    if(search.length > 1){
      $.getJSON("api/sport/city?city="+search).done(function(d){
        var list = []
        if(isFinite(search[0])){
        // Display POSTCODE - City
          list = d.map(function(i){return i.ComInsee + " " + i.ComLib})
        }else{
        // Display City
          list = d.map(function(i){return i.ComLib})
        }

        $("datalist#loc").empty()
        for(c of list) $("datalist#loc").append('<option value="'+ c +'">')
      })
    }
  }

  // // Activities autocomplete
  // $("input.act")[0].oninput = function(){
  //   var search = $(this).val()
  //   if(search.length > 0){
  //     $.getJSON("api/sport/activity?activity="+search).done(function(d){
  //       var list = []
  //       if(isFinite(search[0])){
  //       // Display POSTCODE - City
  //         list = d.map(function(i){return i.ComInsee + " " + i.ComLib})
  //       }else{
  //       // Display City
  //         list = d.map(function(i){return i.ComLib})
  //       }
  //
  //       $("datalist#loc").empty()
  //       for(c of list) $("datalist#loc").append('<option value="'+ c +'">')
  //     })
  //   }
  // }
})
