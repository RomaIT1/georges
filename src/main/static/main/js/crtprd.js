class Cart {
   // ***Елементи HTML статичні
   $orderContainer = document.querySelectorAll('[data-order-container]')
   $cartTotalPrice = document.querySelector('[data-cart-total-price]')
   $cartDeliveryPrice = document.querySelector('[data-cart-delivery-price]')
   $cartTotalAmount = document.querySelector('[data-cart-total-amount]')
   $cartProductsRoot = document.querySelector('#cart-products-root')
   $cartMessage = document.querySelector('#cart-message')
   $cartForm = document.querySelector('#cart-from')
   $cartDetailsField = document.querySelector('#cart-details-field')
   $cartAmountField = document.querySelector('#cart-amount-field')
   $cartUserAgentField = document.querySelector('#cart-user-agent-field')
   // Комбо змінні
   $comboQuestion = document.querySelectorAll('[data-combo-question]')
   $comboForm = document.querySelector('#combo-form')
   $comboTotalPrice = document.querySelector('[data-combo-total-price]')
   // Елементи HTML динамічні (додаються за допомогою рендеру)
   $cartContainer = null
   $pickupCheckbox = document.querySelector('#id_self_pickup')
   currentHour = (new Date()).getHours() 

   // ***Змінні
   deliveryPrice = 40
   deliveryFreePrice = 400
   StorageName = 'CartStoress'
   // Об'єкт корзини
   CartStorage = JSON.parse(localStorage.getItem(this.StorageName)) ? JSON.parse(localStorage.getItem(this.StorageName)) : {
      totalAmount: 0,
      totalPrice: this.deliveryPrice,
      products: [],
      delivery: this.deliveryPrice,
   }
   
   // Ініціалізація
   init(){
      this.checkDeliveryPay()

      // Рендер сторінки
      this.renderCartProducts()
      this.renderTotalAmount()
      this.renderTotalPrice()
      this.renderDeliveryPrice()

      // З'являється повідомлення, якщо кошик порожній
      this.messageIfCartEmpty()
      
      // Додавання події до select комбо
      this.$comboQuestion.forEach(($question, id) => {
         const $select = $question.querySelector('select')
         $select.addEventListener('input', this.changeProductCombo.bind(this, id))
      })
      
      if (this.currentHour < END_WORK_TIME && this.currentHour >= START_WORK_TIME){
         // З'являється форма, якщо кошик не порожній
         this.showForm()
   
         // Записати деталі замовлення в поле
         this.writeDetailsField()
   
         // Записати загальну вартість замовлення в поле
         this.writeAmountField()
         
         // Запис інфи про клієнта в поле
         this.writeUserAgentField()
   
         // Якщо є товари в корзині
         if (this.CartStorage.products.length){
            // Визначення усіх динамічних змінних
            this.#defineDinamicData()
            // Дадавання подій до динамічних елементів
            this.#addListenerDinamicElement()
         }

         this.$pickupCheckbox.addEventListener('input', event => {
            this.checkDeliveryPay()
            this.renderDeliveryPrice()
            this.renderTotalPrice()
         })
         
         // Подія відправки форми
         this.$cartForm.addEventListener('submit', this.sendForm.bind(this))
   
         // Додавання події до кнопок "додати товар в корзину"
         this.$orderContainer.forEach(($container, id) => {
            const $orderButtonAdd = $container.querySelector('[data-order-button-add]')
            if ($orderButtonAdd){
               $orderButtonAdd.addEventListener('click', this.addCartProduct.bind(this, id)) 
            }
         })
   
         // Додавання ідентифікатору до комбо форми та зміна прайсу за комбо
         if (this.$comboForm){
            // Рендер даних на старті сторінки
            this.changeProductCombo()
            // Додавання події до кнопки додати в кошик комбо
            this.$comboForm.addEventListener('submit', this.addProductCombo.bind(this))
         }   
   }
   
      else {
         document.body.insertAdjacentHTML('beforeend', `
         <div class="message error">
            <div class="container">
               <div class="message__inner">
                  Зараз доставка не працює. Ми працюємо з ${START_WORK_TIME}:00 до ${END_WORK_TIME}:00
               </div>
            </div>
         </div>
         `)
      }
   }
   sendForm(){
      this.cartNullProducts()
   }
   cartNullProducts(){
      localStorage.removeItem(this.StorageName)
   }
   // Додавання товару в корзину
   addCartProduct(index){
      // Ідендифікатор товару (унікальний)
      const productId = +this.$orderContainer[index].dataset.orderContainer

      // Якщо такий товар вже є в корзині
      if (this.checkRepeatProduct(productId)){
         // Пошук елемента, який повторюється
         const currentProduct = this.findElement(productId)
         
         // Зміна кількості одного типу товару
         this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].amount++
         
         // Зміна ціни за товар
         this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].totalPrice = this.calculateTotalProductPrice(currentProduct)
         
         // Зміна загальної ціни корзини
         this.CartStorage.totalPrice += this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].currentPrice
      } 
      // Якщо такого товару немає в корзині
      else {
         // Деталі товару (name)
         const $orderFeatureName = this.$orderContainer[index].querySelectorAll('[data-order-product-feature-name]')

         // Деталі товару (value)
         const $orderFeatureValue = this.$orderContainer[index].querySelectorAll('[data-order-product-feature-value]')

         // Об'єкт нового продукту (пустий)
         const newProduct = {}

         // Додавання унікального ідентифікатору до товару
         newProduct.id = productId
         // Додавання імені товару
         newProduct.name = this.$orderContainer[index].querySelector('[data-order-product-name]').textContent
         // Додавання ціни за товар
         newProduct.currentPrice = +this.$orderContainer[index].querySelector('[data-order-product-price]').textContent
         // Дадавання ціни загальної
         newProduct.totalPrice = +this.$orderContainer[index].querySelector('[data-order-product-price]').textContent
         // Додавання деталей
         newProduct.details = []
         // Додавання кількості товару
         newProduct.amount = 1
         // Додавання картинки
         newProduct.image = this.$orderContainer[index].querySelector('[data-order-product-image]').getAttribute('src')
         // Заповлення усіх деталей товару
         $orderFeatureName.forEach(($name, id) => {
            newProduct.details.push({
               name: $name.textContent,
               value: $orderFeatureValue[id].textContent,
            })
         })
         // Додавання товару в список
         this.addProductCartList(newProduct)
         // Додавання загальної ціни товарів в корзині
         this.CartStorage.totalPrice += this.calculateTotalProductPrice(newProduct)
      }

      // ***Завжди виконується при додаванні товару
      // Додавання загальної кількості товарів в корзині
      this.CartStorage.totalAmount++
      
      this.checkDeliveryPay()

      // Оновлення локального сховища
      this.updateStorage()
      // Рендер сторінки
      this.renderCartProducts()
      this.renderTotalAmount()
      this.renderTotalPrice()
      this.renderDeliveryPrice()
      // Визначення усіх динамічних змінних
      this.#defineDinamicData()
      // Дадавання подій до динамічних елементів
      this.#addListenerDinamicElement()
      // З'являється повідомлення, якщо кошик порожній
      this.messageIfCartEmpty()
      // З'являється форма, якщо кошик не порожній
      this.showForm()
      // Записати деталі замовлення в поле
      this.writeDetailsField()
      // Записати загальну вартість замовлення в поле
      this.writeAmountField()
      this.writeUserAgentField()
      
      fbq('track', 'AddToCart', {
         value: `${this.CartStorage.totalPrice}`,
         currency: 'UAH',
         content_ids: '',
         content_type: 'product',
      })
   }
   checkDeliveryPay(){
      if (this.$pickupCheckbox.checked){
         if (this.CartStorage.delivery !== 0){
            this.CartStorage.delivery = 0
            this.CartStorage.totalPrice = this.CartStorage.totalPrice - this.deliveryPrice
         }

         return
      }

      if (this.CartStorage.totalPrice - this.deliveryPrice >= this.deliveryFreePrice){
         if (this.CartStorage.delivery !== 0){
            this.CartStorage.totalPrice -= this.deliveryPrice
         }

         this.CartStorage.delivery = 0
      } 
      
      else {
         if (this.CartStorage.delivery !== this.deliveryPrice){
            this.CartStorage.totalPrice += this.deliveryPrice
         }

         this.CartStorage.delivery = this.deliveryPrice
      }
   }
   checkRepeatProduct(productId){
      let status = false

      for (let product of this.CartStorage.products){
         if (product.id === productId){
            status = true
            break
         }
      }

      return status
   }
   renderCartProducts(){
      this.$cartProductsRoot.innerHTML = ''
      
      function _createDetailsString(product){
         let detailsHTML = ''

         product.details.forEach((detail) => {
            detailsHTML += `
               <div class="cart-products__features-item">
                  <dt>${detail.name}</dt>
                  :
                  <dd>${detail.value}</dd>
               </div>
            `
         })

         return detailsHTML
      }

      this.CartStorage.products.forEach(product => {
         this.$cartProductsRoot.insertAdjacentHTML('afterbegin', `
            <li class="cart-products__item" data-cart-container="${product.id}">
               <div class="cart-products__info">
                  <div class="cart-products__main">
                     <div class="cart-products__image">
                        <img src="${product.image}" alt="cart image">
                     </div>
                     <div class="cart-products__name">${product.name}</div>
                  </div>
                  <dl class="cart-products__features">
                     ${_createDetailsString(product)}
                  </dl>
               </div>
               <div class="cart-products__action">
                  <div class="cart-products__counter products-counter">
                     <button class="products-counter__minus" data-cart-product-button-minus>-</button>
                     <span class="products-counter__value">${product.amount}</span>
                     <button class="products-counter__plus" data-cart-product-button-plus>+</button>
                  </div>
                  <div class="cart-products__price">
                     <span data-cart-product-price>${product.totalPrice}</span>грн
                  </div>
                  <button class="cart-products__remove close-icon" data-cart-product-button-remove>
                     <span></span>
                  </button>
               </div>
            </li>
         `)
      })
   }
   renderTotalPrice(){
      this.$cartTotalPrice.textContent = this.CartStorage.totalPrice
   }
   renderDeliveryPrice(){
      console.log('laskf')
      this.$cartDeliveryPrice.textContent = this.CartStorage.delivery
   }
   renderTotalAmount(){
      this.$cartTotalAmount.textContent = this.CartStorage.totalAmount
   }
   addProductCartList(product){
      this.CartStorage.products.push(product)
   }
   updateStorage(){
      localStorage.setItem(this.StorageName, JSON.stringify(this.CartStorage))
   }
   calculateTotalProductPrice(product){
      return product.currentPrice * product.amount
   }
   #defineDinamicData(){
      this.$cartContainer = document.querySelectorAll('[data-cart-container]')
   }
   // пошук елемента по його індексу
   findElement(id){
      for (let product of this.CartStorage.products){
         if (product.id === id){
            return product
         }
      }
   }
   productRemove(index){
      // Ідентифікатор товару (унікальний)
      const productId = this.$cartContainer[index].dataset.cartContainer.length === 4 ? this.$cartContainer[index].dataset.cartContainer : +this.$cartContainer[index].dataset.cartContainer

      // Видалений елемент з масиву
      let deleteElement = this.findElement(productId)

      // Видалення елементу з списку
      this.CartStorage.products.splice(this.CartStorage.products.indexOf(deleteElement), 1)


      // Зміна значення загальної кількості корзини
      this.CartStorage.totalAmount -= deleteElement.amount
      // Зміна значення загального ціни корзини
      this.CartStorage.totalPrice -= deleteElement.totalPrice

      this.checkDeliveryPay()
      // Оновлення сховища
      this.updateStorage()

      // Рендер
      this.renderCartProducts()
      this.renderTotalAmount()
      this.renderTotalPrice()
      this.renderDeliveryPrice()

      // Визначення усіх динамічних змінних
      this.#defineDinamicData()
      // Дадавання подій до динамічних елементів
      this.#addListenerDinamicElement()

      // З'являється повідомлення, якщо кошик порожній
      this.messageIfCartEmpty()

      // З'являється форма, якщо кошик не порожній
      this.showForm()

      // Записати деталі замовлення в поле
      this.writeDetailsField()

      // Записати загальну вартість замовлення в поле
      this.writeAmountField()
      this.writeUserAgentField()
   }
   // Зміна кількості одного товару
   productSetAmount(index, mode){
      // Ідентифікатор товару (унікальний)
      const productId = this.$cartContainer[index].dataset.cartContainer.length === 4 ? this.$cartContainer[index].dataset.cartContainer : +this.$cartContainer[index].dataset.cartContainer

      // продукт, який змінює свою кількість
      let productSetter = this.findElement(productId)
   
      // Якщо збільшуємо кількість товарів
      if (mode === '+'){
         this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].amount++
         this.CartStorage.totalAmount++
         this.CartStorage.totalPrice += this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].currentPrice
         this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].totalPrice += this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].currentPrice
      } 

      // Якщо зменшуємо кількість товарів
      else if (mode === '-'){
         // Якщо кількість товару дорівнює 1
         if (productSetter.amount === 1){
            this.CartStorage.products.splice(this.CartStorage.products.indexOf(productSetter), 1)
         } 

         // Якщо кількість товару більше 1
         else {
            this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].amount--
            this.CartStorage.products[this.CartStorage.products.indexOf(productSetter)].totalPrice -= productSetter.currentPrice
         }

         this.CartStorage.totalAmount--
         this.CartStorage.totalPrice -= productSetter.currentPrice
      }

      this.checkDeliveryPay()
      // Оновлення сховища
      this.updateStorage()

      // Рендер
      this.renderCartProducts()
      this.renderTotalAmount()
      this.renderTotalPrice()
      this.renderDeliveryPrice()

      // Визначення усіх динамічних змінних
      this.#defineDinamicData()
      // Дадавання подій до динамічних елементів
      this.#addListenerDinamicElement()

      // З'являється повідомлення, якщо кошик порожній
      this.messageIfCartEmpty()

      // З'являється форма, якщо кошик не порожній
      this.showForm()

      // Записати деталі замовлення в поле
      this.writeDetailsField()

      // Записати загальну вартість замовлення в поле
      this.writeAmountField()
      this.writeUserAgentField()
   }
   #addListenerDinamicElement(){
      this.$cartContainer.forEach(($container, id) => {
         const $cartProductButtonRemove = $container.querySelector('[data-cart-product-button-remove]')
         const $cartProductButtonPlus = $container.querySelector('[data-cart-product-button-plus]')
         const $cartProductButtonMinus = $container.querySelector('[data-cart-product-button-minus]')

         $cartProductButtonRemove.addEventListener('click', this.productRemove.bind(this, id))
         $cartProductButtonPlus.addEventListener('click', this.productSetAmount.bind(this, id, '+'))
         $cartProductButtonMinus.addEventListener('click', this.productSetAmount.bind(this, id, '-'))
      })
   }
   messageIfCartEmpty(){
      if (!this.CartStorage.products.length){
         this.$cartMessage.innerHTML = 'Ваш кошик пустий. Покладіть туди щось :)'
      } 

      else {
         this.$cartMessage.innerHTML = ''
      }
   }
   showForm(){
      if (this.CartStorage.products.length){
         this.$cartForm.classList.add('show')
      } else {
         this.$cartForm.classList.remove('show')
      }
   }
   writeDetailsField(){
      let detailsString = ''

      this.CartStorage.products.forEach(product => {
         detailsString += `
         ********`
         detailsString += `
         Назва Товару: ${product.name}`
         detailsString += `
         Кількість одиниць: ${product.amount}`
         detailsString += `
         Деталі: 
         `
         product.details.forEach(detail => {
            detailsString += `${detail.name}: ${detail.value}, `
         })
         detailsString += `
         
         Загальна ціна: ${product.totalPrice} 
         `

      })

      this.$cartDetailsField.setAttribute('value', detailsString)
      this.$cartDetailsField.value = detailsString
   }
   writeAmountField(){
      this.$cartAmountField.setAttribute('value', this.CartStorage.totalPrice)
      this.$cartAmountField.value = this.CartStorage.totalPrice
   }
   writeUserAgentField(){
      this.$cartUserAgentField.setAttribute('value', navigator.userAgent)
      this.$cartUserAgentField.value = navigator.userAgent
   }
   generComboId(){
      let id = ''

      this.$comboQuestion.forEach($question => {
         const $options = $question.querySelector('select').querySelectorAll('option')

         for (let [index, $option] of $options.entries()){
            if ($option.selected){
               id += `${index}`
               break
            }
         }
      })

      return id
   }
   calculateComboTotalPrice(){
      let comboTotalPriceValue = 0

      this.$comboQuestion.forEach($question => {
         const $options = $question.querySelector('select').querySelectorAll('option')

         for (let [index, $option] of $options.entries()){
            if ($option.selected){
               comboTotalPriceValue += +$option.dataset.comboProductPrice
               break
            }
         }
      })

      return comboTotalPriceValue
   }
   changeProductCombo(){
      this.$comboTotalPrice.textContent = this.calculateComboTotalPrice()
   }
   createNameComboProduct(){
      let comboProductName = ''

      this.$comboQuestion.forEach($question => {
         const $options = $question.querySelector('select').querySelectorAll('option')

         for (let [index, $option] of $options.entries()){
            if ($option.selected){
               comboProductName += `${$option.textContent.trim()}, `
               break
            }
         }
      })

      comboProductName = comboProductName.substring(0, comboProductName.length - 2)

      return comboProductName
   }
   getCurrentComboPhoto(){
      let photoCombo = ''

      const $options = this.$comboQuestion[0].querySelectorAll('option')

      for (let $option of $options){
         if ($option.selected){
            photoCombo = $option.dataset.comboProductImage
            break
         }
      }

      return photoCombo
   }
   addProductCombo(event){
      if (event){
         event.preventDefault()
      }
      
      const productId = this.generComboId()

      if (this.checkRepeatProduct(productId)){
         // Пошук елемента, який повторюється
         const currentProduct = this.findElement(productId)
         
         // Зміна кількості одного типу товару
         this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].amount++
         
         // Зміна ціни за товар
         this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].totalPrice = this.calculateTotalProductPrice(currentProduct)
         
         // Зміна загальної ціни корзини
         this.CartStorage.totalPrice += this.CartStorage.products[this.CartStorage.products.indexOf(currentProduct)].currentPrice
      } else {
         const newProduct = {}

         newProduct.id = productId
         newProduct.name = this.createNameComboProduct()
         newProduct.currentPrice = this.calculateComboTotalPrice()
         newProduct.totalPrice = newProduct.currentPrice
         newProduct.image = this.getCurrentComboPhoto()
         newProduct.amount = 1
         newProduct.details = [
            {
               name: 'Ціна',
               value: `${newProduct.currentPrice}`,
            },
         ]

         // Додавання товару в список
         this.addProductCartList(newProduct)
         // Додавання загальної ціни товарів в корзині
         this.CartStorage.totalPrice += this.calculateTotalProductPrice(newProduct)
      }

      // ***Завжди виконується при додаванні товару
      // Додавання загальної кількості товарів в корзині
      this.CartStorage.totalAmount++

      this.checkDeliveryPay()
      // Оновлення локального сховища
      this.updateStorage()
      // Рендер сторінки
      this.renderCartProducts()
      this.renderTotalAmount()
      this.renderTotalPrice()
      this.renderDeliveryPrice()
      // Визначення усіх динамічних змінних
      this.#defineDinamicData()
      // Дадавання подій до динамічних елементів
      this.#addListenerDinamicElement()
      // З'являється повідомлення, якщо кошик порожній
      this.messageIfCartEmpty()
      // З'являється форма, якщо кошик не порожній
      this.showForm()
      // Записати деталі замовлення в поле
      this.writeDetailsField()
      // Записати загальну вартість замовлення в поле
      this.writeAmountField()
      this.writeUserAgentField()
   }
}

const cart = new Cart()

cart.init()