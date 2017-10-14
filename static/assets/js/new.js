function readURL(input) {
	if (input.files && input.files[0]){
		var reader = new FileReader();
		reader.onload = function(e){
				$('#preview').attr('src', e.target.result);
		}
		reader.readAsDataURL(input.files[0]);
	}
}

$('#photo-file').change(function(){
	readURL(this);
});


$('#form').submit(function(){
	$('#add').prop('disabled', true);
	$('#find').prop('disabled', true);
});
