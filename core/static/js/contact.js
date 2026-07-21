const alert_element = document.getElementById("alert_element");

if (alert_element && alert_element.dataset.state == "success") {

    Toastify({
        text: "پیام شما با موفقیت ارسال شد !",
        gravity: "top",
        position: "left",
        style: {
            color : "#fff",
            background: "#009689",
        }
    }).showToast();

} else if (alert_element && alert_element.dataset.state == "fail") {
    Toastify({
        text: "متاسفانه در ارسال پیام مشکلی پیش آمد",
        gravity: "top",
        position: "left",
        style: {
            color : "#fff",
            background: "#ff0000",
        }
    }).showToast();
}
