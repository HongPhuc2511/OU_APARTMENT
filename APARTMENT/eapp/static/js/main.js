function addToCart(id,name,price,area,apartment_type,image){
    fetch('/api/cart',{
        method:'post',
        body:JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'area': area,
            'apartment_type': apartment_type,
            'image': image
        }),
        headers:{
            'Content-Type':'application/json'
        }
    }).then(res=>res.json())
        .then(data=>{
        let eles =document.getElementsByClassName("cart-counter");
        for (let e of eles)
        e.innerText=data.total_quantity;

        alert(data.message);
    });
}

function deleteCart(id,quantity){
       fetch(`/api/cart/${id}`, {
        method: 'delete'
    })
    .then(res => res.json())
    .then(data => {
        let eles = document.getElementsByClassName("cart-counter");
        for (let e of eles)
            e.innerText = data.total_quantity;

        let row = document.getElementById(`cart-item-${id}`);
        if (row) row.remove();

        let totalEl = document.getElementById("cart-total");
        if (totalEl) totalEl.innerText = data.total_amount.toLocaleString() + " VNĐ";
    })
    .catch(err => {
        console.error(err);
        alert("Không thể xóa căn hộ!");
    });
}

//    if(confirm("Bạn chắc chắn thanh toán?")=== true){
//        fetch("/api/pay",{
//            method:"post"
//        })
//        .then(res => res.json()).then(res=>{
//            if(res.status===200)
//            location.reload();
//            else
//            alert("Hệ thống bị lỗi!");
//        })
//    }
function pay(){

      const method = document.querySelector(
        'input[name="paymentMethod"]:checked'
    ).value;

    fetch('/api/pay', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ payment_method: method })
    })


        .then(res => res.json())
        .then(data => {
        if (data.status === 200) {
            alert('Thanh toán thành công!Vui lòng chờ xác nhận . Xem chi tiết ở thông tin hợp đồng');

            window.location.reload();
        } else {
            alert('Thanh toán thất bại');
        }
    });
}
//
//function pay() {
//    const methodInput = document.querySelector('input[name="paymentMethod"]:checked');
//
//    if (!methodInput) {
//        alert("Vui lòng chọn phương thức thanh toán!");
//        return;
//    }
//    const method = methodInput.value;
//
//    fetch('/api/pay', {
//        method: 'post',
//        headers: { 'Content-Type': 'application/json' },
//        body: JSON.stringify({ payment_method: method })
//    })
//
//    .then(data => {
//        if (data.status === 200) {
//            alert('Thanh toán thành công! Vui lòng chờ xác nhận.');
//            window.location.reload();
//        } else {
//            alert('Lỗi: ' + data.error);
//        }
//    })
//    .catch(err => {
//        console.error("Chi tiết lỗi:", err);
//        alert('Thanh toán thất bại. Hãy kiểm tra Console (F12) để xem chi tiết.');
//    });
//}

