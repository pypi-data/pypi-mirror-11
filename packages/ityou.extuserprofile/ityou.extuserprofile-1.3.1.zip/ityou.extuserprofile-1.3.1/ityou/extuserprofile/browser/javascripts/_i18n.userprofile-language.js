var userprofile_language_en = { 
    "choose_image"		: "Choose image to crop",
    "crop_image"		: "Crop image",
    "click_to_edit"		: "Click to edit...",
    "date_placeholder"	: "DD.MM.YYYY"
}

var userprofile_language_de = { 
    "choose_image"  	: "Bild zum Zuschneiden auswählen",
    "crop_image"		: "Bild zuschneiden",
	"click_to_edit"		: "Anklicken zum Bearbeiten",
	"date_placeholder"	: "TT.MM.JJJJ"
}


$(document).ready(
				
    function () {
        // --- initialize i18n
        
        i18n_language = $('html').attr("lang").slice(0,2);
    }
);
