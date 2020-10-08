<?php
$pdo=new PDO('mysql:host=localhost;port=8889;dbname=sample;','dharun','zap');
$pdo->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
$sm=$pdo->prepare('SELECT Attendance from class');
$sm->execute();
$row1=$sm->fetch(PDO::FETCH_ASSOC);
$count1=0;
$count2=0;
while($row1)
{
  if(strtolower($row1['Attendance'])=="present")
  {
    $count1+=1;
  }
  else if(strtolower($row1['Attendance'])=="absent") {
    $count2+=1;
  }
  $row1=$sm->fetch(PDO::FETCH_ASSOC);
}
$smtp=$pdo->prepare('SELECT COUNT(id) as count FROM class');
$smtp->execute();
$row=$smtp->fetch(PDO::FETCH_ASSOC);
if($row)
{
  $data=array('count'=>$row['count'],'count1'=>$count1,'count2'=>$count2);
  echo json_encode($data);
}
?>
