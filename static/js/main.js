function gmailAuthenticate() {
    $.ajax({
        type: "GET",
        url: "ajax/gmailAuthenticate",
        success: function (data) {
            console.log('Done')
        }
    });
};

// Ajax call to Django