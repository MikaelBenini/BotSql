<?php
require_once '../vendor/autoload.php';
require_once '../vendor/phpoffice/phpexcel/Classes/PHPExcel.php';

// configuração da conexão com o banco de dados
$servername = "mysql.senhafacil.net.br";
$username = "senhafacil";
$password = "Reimisterio145";
$dbname = "senhafacil";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

if(isset($_FILES['file']['name']))
{
    $file_name = $_FILES['file']['name'];
    $file_tmp =$_FILES['file']['tmp_name'];
    $ext = pathinfo($file_name, PATHINFO_EXTENSION);

    if($ext == "xlsx")
    {
        $excelReader = PHPExcel_IOFactory::createReaderForFile($file_tmp);
        $excelObj = $excelReader->load($file_tmp);
        $worksheet = $excelObj->getSheet(0);
        $lastRow = $worksheet->getHighestRow();
        $result = false;
        for ($row = 2; $row <= $lastRow; $row++) {
            $codigo = $worksheet->getCell('A'.$row)->getValue();
            // inserir o código no banco de dados
            $sql = "INSERT INTO Codigo (codigos) VALUES ('$codigo')";

            if ($conn->query($sql) === TRUE) {
                $result = true;
            } else {
                echo "Erro ao inserir código: " . $conn->error;
            }
        }
        if($result) {
            echo "<script>alert('Códigos inseridos com sucesso.'); window.location = '../index.html';</script>";
        }
    }
    else
    {
        echo "Por favor, selecione um arquivo com extensão .xlsx";
    }
}
else
{
    echo "Por favor, selecione um arquivo.";
}

// Fecha a conexão com o banco de dados
$conn->close();

?>
