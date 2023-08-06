function cambia_permiso()
{
  var permiso_id = $(this).val();
  var django_user_id = $("#django_user_id").val();
  var checked = $(this).attr('checked') === 'checked';
  
  $.ajax({
    url:'/administrador/change_user_permission/',
    type : 'get',
    data:{
      'permiso_id' : permiso_id,
      'django_user_id': django_user_id,
      'checked':checked
    },
    error: function() {
      alert('algo fallo');
    },
  });
}

$(".permiso_chbox").on('change', cambia_permiso);