function(value){
    {% for term in view.terms %}
        if(value == '${term.token}'){
          return '${term.title}';
        }
    {% end %}
    return '';
}