import { useState } from 'react';
import { Form, Input, Select } from 'antd';
import { ArrowRightOutlined } from '@ant-design/icons';
import styles from './ConversationalForm.module.css';
import '../antd-select-override.css';

export const questions = [
  {
    key: 'nome',
    label: '👋 Como você deseja ser chamado?',
    type: 'text',
    rules: [
      { required: true, message: 'Por favor, informe o nome ou apelido.' },
      {
        validator: (_, value) => {
          if (value && value.length < 2) {
            return Promise.reject('Nome muito curto. Informe pelo menos 2 caracteres.');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: { placeholder: 'Digite o nome ou apelido 😊' },
  },
  {
    key: 'age',
    label: '🎂 Qual a sua idade?',
    type: 'number',
    rules: [
      { required: true, message: 'Idade obrigatória' },
      {
        validator: (_, value) => {
          const num = Number(value);
          if (!value || isNaN(num) || num < 1 || num > 120) {
            return Promise.reject('Idade inválida');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: { min: 1, max: 120, placeholder: 'Ex: 35' },
  },
  {
    key: 'gender',
    label: '🧑‍⚕️ Qual o seu gênero?',
    type: 'select',
    options: [
      { value: 'male', label: 'Masculino 👨' },
      { value: 'female', label: 'Feminino 👩' },
      { value: 'other', label: 'Outro 🧑' },
    ],
    rules: [{ required: true, message: 'Selecione o gênero' }],
  },
  {
    key: 'height',
    label: '📏 Qual a sua altura (cm)?',
    type: 'number',
    rules: [
      { required: true, message: 'Altura obrigatória' },
      {
        validator: (_, value) => {
          const num = Number(value);
          if (!value || isNaN(num) || num < 50 || num > 250) {
            return Promise.reject('Altura inválida');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: { min: 50, max: 250, placeholder: 'Ex: 168' },
  },
  {
    key: 'weight',
    label: '⚖️ Qual o seu peso (kg)?',
    type: 'float',
    rules: [
      { required: true, message: 'Peso obrigatório' },
      {
        validator: (_, value) => {
          const num = parseFloat(value);
          if (!value || isNaN(num) || num < 20 || num > 300) {
            return Promise.reject('Peso inválido');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: { min: 20, max: 300, step: 0.1, inputMode: 'decimal', pattern: '[0-9]+([.,][0-9]{1,2})?', placeholder: 'Ex: 72.5' },
  },
  {
    key: 'smoker',
    label: '🚬 Você é fumante?',
    type: 'select',
    options: [
      { value: true, label: 'Sim 👍' },
      { value: false, label: 'Não 👎' },
    ],
    rules: [{ required: true, message: 'Selecione uma opção' }],
  },
];

export function ConversationalForm({ step, onStep }) {
  const [form] = Form.useForm();
  const current = questions[step];

  // Estado para guardar o nome do usuário após o primeiro passo
  const [nomeUsuario, setNomeUsuario] = useState('');

  // Atualiza o nome do usuário após o primeiro passo
  const nomeForm = Form.useWatch('nome', form);
  // Atualiza o estado apenas no passo 0, quando o nome é informado
  if (step === 0 && nomeForm && nomeForm !== nomeUsuario) {
    setNomeUsuario(nomeForm);
  }

  // Textos intermediários personalizados
  const interTexts = [
    'Que bom te conhecer! 😊 Vamos começar sua jornada de saúde.',
    nomeUsuario ? `Perfeito, ${nomeUsuario}! Agora me conte sua idade. Isso é essencial para sua análise! 🎂` : 'Perfeito! Agora me conte sua idade. Isso é essencial para sua análise! 🎂',
    nomeUsuario ? `Ótimo, ${nomeUsuario}! Qual o seu gênero? O algoritmo considera isso na sua avaliação. 🧑‍⚕️` : 'Ótimo! Qual o seu gênero? O algoritmo considera isso na sua avaliação. 🧑‍⚕️',
    nomeUsuario ? `Excelente, ${nomeUsuario}! Sua altura nos ajuda a calcular métricas importantes para você. 📏` : 'Excelente! Sua altura nos ajuda a calcular métricas importantes para você. 📏',
    nomeUsuario ? `Quase terminando, ${nomeUsuario}! Agora preciso saber seu peso. ⚖️` : 'Quase terminando! Agora preciso saber seu peso. ⚖️',
    nomeUsuario ? `Última pergunta, ${nomeUsuario}! Você fuma? Isso impacta significativamente no seu risco cardíaco. 🚬` : 'Última pergunta! Você fuma? Isso impacta significativamente no seu risco cardíaco. 🚬',
  ];
  const handleNext = (values) => {
    const value = values[current.key];
    let isValid = true;
    let errorMsg = '';
    if (current.type === 'number') {
      const num = Number(value);
      if (!value || isNaN(num) || num < (current.inputProps?.min ?? 1) || num > (current.inputProps?.max ?? 999)) {
        isValid = false;
        errorMsg = `Valor inválido para ${current.label.toLowerCase()}.`;
      }
    }
    if (current.type === 'select') {
      if (typeof value === 'undefined' || !current.options.some(opt => opt.value === value)) {
        isValid = false;
        errorMsg = `Seleção inválida para ${current.label.toLowerCase()}.`;
      }
    }
    let displayValue = value;
    if (current.type === 'select') {
      const selected = current.options.find(opt => opt.value === value);
      if (selected) displayValue = selected.label;
    }
    // Salva o nome do usuário no estado ao finalizar o primeiro passo
    if (current.key === 'nome' && value) {
      setNomeUsuario(value);
    }
    // Chama o callback para avançar o passo
    if (typeof onStep === 'function') {
      onStep(displayValue, isValid ? null : errorMsg);
    }
    // Limpa o campo para o próximo passo, exceto o nome
    if (current.key !== 'nome') {
      form.resetFields();
    }
  };

  return (
    <div key={step} className="animate-slide-in-right" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'flex-end', 
      marginBottom: 'var(--space-3)',
      position: 'relative'
    }}>
      {/* Texto intermediário com design moderno */}
      <div key={step} className="animate-fade-in" style={{ 
        fontSize: '1rem',
        color: 'var(--neutral-600)',
        marginBottom: 'var(--space-3)',
        textAlign: 'right',
        fontWeight: 500,
        lineHeight: 1.4,
        background: 'linear-gradient(135deg, rgba(24, 144, 255, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%)',
        padding: 'var(--space-2) var(--space-4)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid rgba(24, 144, 255, 0.1)',
        backdropFilter: 'blur(10px)'
      }}>
        {interTexts[step]}
      </div>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleNext}
        style={{ 
          maxWidth: 380, 
          minWidth: 240, 
          width: '100%', 
          margin: 0 
        }}
        onKeyDown={e => {
          if (e.key === 'Enter') {
            e.preventDefault();
            form.submit();
          }
        }}
      >
        {current.type === 'text' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }}>
            <Input
              type="text"
              size="large"
              autoFocus
              placeholder={current.inputProps?.placeholder || 'Escreva aqui...'}
              style={{ 
                fontSize: '1.125rem',
                padding: 'var(--space-4) var(--space-5)',
                borderRadius: 'var(--radius-lg)',
                border: '2px solid rgba(24, 144, 255, 0.1)',
                background: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)'
              }}
            />
          </Form.Item>
        )}
        {current.type === 'number' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }}>
            <Input
              type="number"
              size="large"
              {...current.inputProps}
              autoFocus
              placeholder="Digite aqui..."
              style={{ 
                fontSize: '1.125rem',
                padding: 'var(--space-4) var(--space-5)',
                borderRadius: 'var(--radius-lg)',
                border: '2px solid rgba(24, 144, 255, 0.1)',
                background: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)'
              }}
            />
          </Form.Item>
        )}
        {current.type === 'float' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }}>
            <Input
              type="text"
              size="large"
              inputMode="decimal"
              pattern="[0-9]+([.,][0-9]{1,2})?"
              autoFocus
              placeholder="Ex: 72.5"
              style={{ 
                fontSize: '1.125rem',
                padding: 'var(--space-4) var(--space-5)',
                borderRadius: 'var(--radius-lg)',
                border: '2px solid rgba(24, 144, 255, 0.1)',
                background: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)'
              }}
              onChange={e => {
                // Mascara: permite apenas números e ponto ou vírgula
                const val = e.target.value.replace(/[^0-9.,]/g, '');
                form.setFieldsValue({ [current.key]: val });
              }}
              onBlur={e => {
                // Normaliza para ponto
                const val = e.target.value.replace(',', '.');
                form.setFieldsValue({ [current.key]: val });
              }}
            />
          </Form.Item>
        )}
        {current.type === 'select' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }}>
            <div style={{
              display: 'flex',
              gap: 'var(--space-3)',
              flexWrap: 'wrap',
              justifyContent: 'flex-end',
              marginBottom: 'var(--space-3)'
            }}>
              {current.options.map(opt => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => {
                    form.setFieldsValue({ [current.key]: opt.value });
                    setTimeout(() => form.submit(), 100); // garante submit após setFieldsValue
                  }}
                  style={{
                    minWidth: 120,
                    padding: 'var(--space-4) var(--space-5)',
                    fontSize: '1.125rem',
                    borderRadius: 'var(--radius-lg)',
                    background: form.getFieldValue(current.key) === opt.value ? 'var(--primary-500)' : 'rgba(255,255,255,0.9)',
                    color: form.getFieldValue(current.key) === opt.value ? '#fff' : 'var(--neutral-900)',
                    fontWeight: 600,
                    border: form.getFieldValue(current.key) === opt.value ? '2px solid var(--primary-500)' : '2px solid rgba(24, 144, 255, 0.1)',
                    boxShadow: form.getFieldValue(current.key) === opt.value ? 'var(--shadow-md)' : 'none',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    outline: 'none',
                    marginBottom: 'var(--space-2)'
                  }}
                  tabIndex={0}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </Form.Item>
        )}
        {/* Botão de submit invisível para garantir envio ao pressionar Enter nos outros campos */}
        {current.type !== 'select' && <button type="submit" style={{ display: 'none' }} />}
      </Form>
      
      {/* Instrução modernizada */}
      <div className="animate-fade-in" style={{ 
        fontSize: '0.875rem',
        color: 'var(--neutral-500)',
        marginTop: 'var(--space-2)',
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-2)',
        fontWeight: 500,
        background: 'rgba(24, 144, 255, 0.05)',
        padding: 'var(--space-2) var(--space-3)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid rgba(24, 144, 255, 0.1)'
      }}>
        <span style={{ 
          background: 'var(--gradient-primary)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          fontWeight: 700
        }}>
          Enter
        </span>
        para enviar
        <span style={{ 
          fontSize: '1.125rem', 
          color: 'var(--primary-500)',
          animation: 'pulse 2s ease-in-out infinite'
        }}>
          ⚡
        </span>
      </div>
    </div>
  );
}
