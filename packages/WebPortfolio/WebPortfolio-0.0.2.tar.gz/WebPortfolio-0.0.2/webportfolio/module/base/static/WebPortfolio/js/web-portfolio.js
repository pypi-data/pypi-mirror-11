
var WebPortfolio = {

    /**
    Google Analytics tracking
    **/
    track_event: function(category, action, label, value) {
        if (typeof ga !== 'undefined') {
            ga("send", "event", category, action, label, value)
        }
    },

    //------

    /**
    BASIC Login
    **/
    basic_login: function() {
        var that = this
        $("#webportfolio-login-login-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "LOGIN", "Email")
            this.submit()
        })
        $("#webportfolio-login-signup-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "SIGNUP", "Email")
            this.submit()
        })
        $("#webportfolio-login-lostpassword-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "LOSTPASSWORD", "Email")
            this.submit()
        })
    },

    /**
     * Setup Authomatic
     */
    setup_authomatic: function(redirect) {
        authomatic.setup({
            onLoginComplete: function(result) {
                switch(result.custom.action) {
                    case "redirect":
                        location.href = result.custom.url
                        break
                    default:
                        if (redirect == "") {
                            redirect = "/"
                        }
                        location.href = redirect
                        break
                }
            }
        })

        authomatic.popupInit()
    }
    
}

$(function(){
    $("img.lazy").lazy({
        effect: "fadeIn",
        effectTime: 1000
    })

    $("a.oembed").oembed();
})
