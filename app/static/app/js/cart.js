var updateBtns = document.getElementsByClassName('update-cart')

for(i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)
        console.log('user: ', user)
        if(user === 'AnonymousUser'){
            alert('Người dùng chưa đăng nhập')
        }else{
            updateUserOrder(productId, action)
        }
       
    })
    
}

// hàm xử lý cập nhật giỏ hàng
function updateUserOrder(productId, action){
    console.log('Người dùng đã đăng nhập, thêm thành công')
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
        
    })
    .then ((response)=>{
        return response.json()        
    })
    .then ((data)=>{
        console.log('data', data)
        location.reload()
    })
}



