
import 'package:flutter/material.dart';
import 'customRaisedButton.dart';

class CartPage extends StatefulWidget {
  @override
  _CartPageState createState() => _CartPageState();
}

class _CartPageState extends State<CartPage> {

  double sum = 0;
  int itemsCount = 0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Cart'),
        ),
        // ignore: unrelated_type_equality_checks
        body: cartList(context)
    );
  }

  Widget cartList(context){
    return SingleChildScrollView(
      physics: ScrollPhysics(),
      child: Column(
        children: <Widget>[

          dataDisplay(context,"TESTKJN@",["BANANA","APPLE"],{'Usrname':33,'Password':22})

        ],
      ),
    );
  }

  Widget dataDisplay(BuildContext context, String uid, List<String> foodIds, Map<String, int> count){
    return FutureBuilder(
        future: null,
      builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
        if (snapshot.hasData ) {
          // Cart cart= new Cart("3232", 232, "itemName", 44, 48787);
          // List<Cart> _cartItems = <Cart>[cart];
          // _cartItems.add(cart);
          //
          // if (_cartItems.length > 0){
          //   sum = 0;
          //   itemsCount= 0;
          //   _cartItems.forEach((element) {
          //     if(element.price != null && element.count != null){
          //       sum += element.price * element.count;
          //       itemsCount += element.count;
          //     }
          //   });
            return Container(
                margin: EdgeInsets.only(top: 10.0),
                child: Column(
                  children: [
                    ListView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: 10,
                        itemBuilder: (context, int i) {
                          return ListTile(
                            title: Text("_cartItems[i].itemName ?? ''"),
                            subtitle: Text("cost:"),
                            trailing: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: <Widget>[
                                  IconButton(
                                    onPressed: () async{
                                    },
                                    icon: new Icon(Icons.remove),
                                  ),
                                  Text(
                                    "fdssssssssss}",
                                    style: TextStyle(fontSize: 18.0),
                                  ),
                                  IconButton(
                                    icon: new Icon(Icons.add),
                                    onPressed: () async{
                                    },
                                  )
                                ]),
                          );
                        }),
                    Text("Total ($itemsCount items): $sum INR"),
                    SizedBox(
                      height: 40,
                    ),
                    GestureDetector(
                      onTap: () {
                      },
                      child: CustomRaisedButton(buttonText: 'Proceed to buy'),
                    ),
                    SizedBox(
                      height: 70,
                    ),
                  ],
                )
            );
          } else {
            return Container(
              padding: EdgeInsets.symmetric(vertical: 20),
              width: MediaQuery.of(context).size.width * 0.6,
              child: Text("No Items to display"),
            );
          }
        }
        // else {
        //
        //   return Container(
        //     padding: EdgeInsets.symmetric(vertical: 20),
        //     width: MediaQuery.of(context).size.width * 0.6,
        //     child: Text("No Items to display"),
        //   );
        // }
      // },
    );
  }

}