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