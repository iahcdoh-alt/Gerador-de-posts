; Script de Instalação para Gerador de Posts Instagram
; Compilar com Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "Gerador de Posts Instagram"
#define MyAppVersion "1.0"
#define MyAppPublisher "Seu Nome/Empresa"
#define MyAppExeName "GeradordePosts_GUI.exe"

[Setup]
; Informações do aplicativo
AppId={{8F9A5B2C-1D4E-4A6B-9C8D-3E7F2A1B5C4D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=GeradordePosts_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; SetupIconFile=icon.ico
; UninstallDisplayIcon={app}\{#MyAppExeName}

; Privilégios
PrivilegesRequired=lowest

; Diretórios
DisableProgramGroupPage=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
; Executável principal
Source: "dist\GeradordePosts_GUI.exe"; DestDir: "{app}"; Flags: ignoreversion

; Pasta generated_images
Source: "dist\generated_images\*"; DestDir: "{app}\generated_images"; Flags: ignoreversion recursesubdirs createallsubdirs

; Arquivo .env de exemplo
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion

; README (se existir)
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"

; Atalho na Área de Trabalho (opcional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Opção de executar após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  EnvPage: TInputQueryWizardPage;
  APIKeyEntered: Boolean;

procedure InitializeWizard;
begin
  APIKeyEntered := False;

  { Criar página para configurar chave da API }
  EnvPage := CreateInputQueryPage(wpSelectDir,
    'Configuração da API OpenAI',
    'Configure sua chave da API',
    'Para usar o aplicativo, você precisa de uma chave da API OpenAI.' + #13#10 +
    'Você pode inserir agora ou configurar depois editando o arquivo .env na pasta de instalação.' + #13#10#13#10 +
    'Obtenha sua chave em: https://platform.openai.com/api-keys');

  EnvPage.Add('Chave da API OpenAI (deixe em branco para configurar depois):', False);
  EnvPage.Values[0] := '';
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  if CurPageID = EnvPage.ID then
  begin
    { Salvar se usuário inseriu chave }
    if EnvPage.Values[0] <> '' then
      APIKeyEntered := True;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvFilePath: String;
  EnvContent: TStringList;
begin
  if CurStep = ssPostInstall then
  begin
    EnvFilePath := ExpandConstant('{app}\.env');

    { Criar arquivo .env }
    EnvContent := TStringList.Create;
    try
      if APIKeyEntered and (EnvPage.Values[0] <> '') then
      begin
        { Usuário forneceu chave }
        EnvContent.Add('# Configuração da API OpenAI');
        EnvContent.Add('OPENAI_API_KEY=' + EnvPage.Values[0]);
        EnvContent.Add('');
        EnvContent.Add('# Gerado automaticamente durante a instalação');
      end
      else
      begin
        { Copiar do .env.example }
        if FileExists(ExpandConstant('{app}\.env.example')) then
        begin
          EnvContent.LoadFromFile(ExpandConstant('{app}\.env.example'));
        end
        else
        begin
          EnvContent.Add('# Configuração da API OpenAI');
          EnvContent.Add('OPENAI_API_KEY=sua_chave_api_aqui');
          EnvContent.Add('');
          EnvContent.Add('# Obtenha sua chave em: https://platform.openai.com/api-keys');
          EnvContent.Add('# Substitua "sua_chave_api_aqui" pela sua chave real');
        end;
      end;

      EnvContent.SaveToFile(EnvFilePath);
    finally
      EnvContent.Free;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DialogResult: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    DialogResult := MsgBox('Deseja manter as imagens geradas e o arquivo de configuração (.env)?',
                           mbConfirmation, MB_YESNO);

    if DialogResult = IDNO then
    begin
      { Remover pasta generated_images }
      DelTree(ExpandConstant('{app}\generated_images'), True, True, True);

      { Remover .env }
      DeleteFile(ExpandConstant('{app}\.env'));
    end;
  end;
end;
