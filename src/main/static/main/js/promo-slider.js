function createPromoSlider(options){
   if (!document.getElementById('promo-slider')) return
   
   const SLIDE_NEXT_INTERVAL = 15000

   const promoSlider = new Swiper('#promo-slider', {
      navigation: {
         nextEl: '.swiper-button-next',
         prevEl: '.swiper-button-prev',
      },
      speed: 1500,
      loop: true,
      pagination: {
         el: '.swiper-pagination',
      },
      autoHeight: true,
      simulateTouch: false,
      touchAngle: 0,
      initialSlide: 1,
      effect: 'flip',
      flipEffect: {
        slideShadows: false,
      },
   })

   if (options){
      if (options.slideInterval){
         setInterval(() => {
            promoSlider.slideNext()
         }, SLIDE_NEXT_INTERVAL)
      }
   }
}

createPromoSlider({
   slideInterval: true,
})