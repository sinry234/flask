$(function(){
	//页面加载完成之后执行
	pageInit();
});
function pageInit(){
	//创建jqGrid组件
	jQuery("#list").jqGrid(
			{
				//url : 'data/JSONData.json',//组件创建完成之后请求数据的url
				datatype : "local",//请求数据返回的类型。可选json,xml,txt
				height : 250, //"100%",
				colNames : [ 'Inv No', 'Date', 'Client', 'Amount', 'Tax','Total', 'Notes' ],//jqGrid的列显示名字
				colModel : [ //jqGrid每一列的配置信息。包括名字，索引，宽度,对齐方式.....
				             {name : 'id',index : 'id',width : 55, sorttype:'integer'}, 
				             {name : 'invdate',index : 'invdate',width : 90, sorttype:'date'}, 
				             {name : 'name',index : 'name asc, invdate',width : 100, sorttype:'text'}, 
				             {name : 'amount',index : 'amount',width : 80,align : "right", sorttype:'integer'}, 
				             {name : 'tax',index : 'tax',width : 80,align : "right", sorttype:'integer'}, 
				             {name : 'total',index : 'total',width : 80,align : "right", sorttype:'integer'}, 
				             {name : 'note',index : 'note',width : 150,sortable : false} 
				           ],
				rowNum : 10,//一页显示多少条
				rowList : [ 10, 20, 30 ],//可供用户选择一页显示多少条
				pager : '#gridpager',//表格页脚的占位符(一般是div)的id
				loadonce:true,
				sortname : 'id',//初始化的时候排序的字段
				sortorder : 'desc',//排序方式,可选desc,asc
				mtype : "get",//向后台请求数据的ajax的类型。可选post,get
				viewrecords : true,
				multiselect : true,
				caption : "JSON Example"//表格的标题名字
			});
	/*创建jqGrid的操作按钮容器*/
	/*可以控制界面上增删改查的按钮是否显示*/
	//jQuery("#list").jqGrid('navGrid', '#gridpager', {edit : false,add : false,del : false});
	plandata = '{{plan_price_ranges2}}'
	for ( var i = 0; i <= plandata.length; i++){
    jQuery("#list").jqGrid('addRowData', i + 1, plandata[i]);
  }
}