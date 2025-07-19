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
    key: 'ap_hi',
    label: '🩺 Pressão sistólica (maior)',
    type: 'number',
    rules: [
      { required: true, message: 'Pressão sistólica obrigatória' },
      {
        validator: (_, value) => {
          const num = Number(value);
          if (!value || isNaN(num) || num < 80 || num > 250) {
            return Promise.reject('Valor inválido para pressão sistólica');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: {
      min: 80,
      max: 250,
      placeholder: 'Ex: 120',
      help: 'A pressão sistólica é o número MAIOR na medição, geralmente entre 100 e 140 para adultos. Se não souber, use o valor do seu último exame ou peça orientação médica.'
    },
  },
  {
    key: 'ap_lo',
    label: '🩺 Pressão diastólica (menor)',
    type: 'number',
    rules: [
      { required: true, message: 'Pressão diastólica obrigatória' },
      {
        validator: (_, value) => {
          const num = Number(value);
          if (!value || isNaN(num) || num < 40 || num > 150) {
            return Promise.reject('Valor inválido para pressão diastólica');
          }
          return Promise.resolve();
        },
      },
    ],
    inputProps: {
      min: 40,
      max: 150,
      placeholder: 'Ex: 80',
      help: 'A pressão diastólica é o número MENOR na medição, geralmente entre 60 e 90 para adultos. Se não souber, use o valor do seu último exame ou peça orientação médica.'
    },
  },
  {
    key: 'cholesterol',
    label: '🧪 Nível de colesterol',
    type: 'select',
    options: [
      { value: 1, label: 'Normal' },
      { value: 2, label: 'Acima do normal' },
      { value: 3, label: 'Muito acima do normal' },
    ],
    rules: [{ required: true, message: 'Selecione o nível de colesterol' }],
  },
  {
    key: 'gluc',
    label: '🧪 Nível de glicose',
    type: 'select',
    options: [
      { value: 1, label: 'Normal' },
      { value: 2, label: 'Acima do normal' },
      { value: 3, label: 'Muito acima do normal' },
    ],
    rules: [{ required: true, message: 'Selecione o nível de glicose' }],
  },
  {
    key: 'alco',
    label: '🍷 Você consome álcool?',
    type: 'select',
    options: [
      { value: 1, label: 'Sim' },
      { value: 0, label: 'Não' },
    ],
    rules: [{ required: true, message: 'Selecione uma opção' }],
  },
  {
    key: 'active',
    label: '🏃 Você pratica atividade física regularmente?',
    type: 'select',
    options: [
      { value: 1, label: 'Sim' },
      { value: 0, label: 'Não' },
    ],
    rules: [{ required: true, message: 'Selecione uma opção' }],
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
    inputProps: { min: 1, max: 120, placeholder: 'Ex: 28' }, // exemplo ajustado
  },
  {
    key: 'gender',
    label: '🧑‍⚕️ Qual o seu gênero?',
    type: 'select',
    options: [
      { value: 2, label: 'Masculino 👨' },
      { value: 1, label: 'Feminino 👩' },
      { value: 3, label: 'Outro 🧑' },
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
    inputProps: { min: 50, max: 250, placeholder: 'Ex: 172' }, // exemplo ajustado
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
    key: 'smoke',
    label: '🚬 Você é fumante?',
    type: 'select',
    options: [
      { value: 1, label: 'Sim 👍' },
      { value: 0, label: 'Não 👎' },
    ],
    rules: [{ required: true, message: 'Selecione uma opção' }],
  },
];

export function ConversationalForm({ step, onStep }) {
  const [form] = Form.useForm();
  const current = questions[step];

  const [nomeUsuario, setNomeUsuario] = useState('');

  const nomeForm = Form.useWatch('nome', form);
  if (step === 0 && nomeForm && nomeForm !== nomeUsuario) {
    setNomeUsuario(nomeForm);
  }

  const interTexts = [
    '👋 Olá! Para começarmos, como você deseja ser chamado?',
    nomeUsuario ? `Ótimo, ${nomeUsuario}! Agora informe sua pressão sistólica (maior). Se não souber, consulte seu último exame ou pergunte ao médico. 🩺` : 'Ótimo! Agora informe sua pressão sistólica (maior). Se não souber, consulte seu último exame ou pergunte ao médico. 🩺',
    nomeUsuario ? `Perfeito, ${nomeUsuario}! Agora informe sua pressão diastólica (menor). 🩺` : 'Perfeito! Agora informe sua pressão diastólica (menor). 🩺',
    nomeUsuario ? `Agora vamos para o colesterol, ${nomeUsuario}. Se não souber, escolha a opção mais próxima. 🧪` : 'Agora vamos para o colesterol. Se não souber, escolha a opção mais próxima. 🧪',
    nomeUsuario ? `E o nível de glicose, ${nomeUsuario}? 🧪` : 'E o nível de glicose? 🧪',
    nomeUsuario ? `Você consome álcool, ${nomeUsuario}? �` : 'Você consome álcool? 🍷',
    nomeUsuario ? `Pratica atividade física regularmente, ${nomeUsuario}? 🏃` : 'Pratica atividade física regularmente? 🏃',
    nomeUsuario ? `Agora sua idade, ${nomeUsuario}. Isso é essencial para sua análise! 🎂` : 'Agora sua idade. Isso é essencial para sua análise! 🎂',
    nomeUsuario ? `Qual o seu gênero, ${nomeUsuario}? O algoritmo considera isso na sua avaliação. 🧑‍⚕️` : 'Qual o seu gênero? O algoritmo considera isso na sua avaliação. 🧑‍⚕️',
    nomeUsuario ? `Sua altura nos ajuda a calcular métricas importantes para você, ${nomeUsuario}. 📏` : 'Sua altura nos ajuda a calcular métricas importantes para você. 📏',
    nomeUsuario ? `Agora preciso saber seu peso, ${nomeUsuario}. ⚖️` : 'Agora preciso saber seu peso. ⚖️',
    nomeUsuario ? `Você é fumante, ${nomeUsuario}? Isso impacta significativamente no seu risco cardíaco. 🚬` : 'Você é fumante? Isso impacta significativamente no seu risco cardíaco. 🚬',
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
    if (current.key === 'nome' && value) {
      setNomeUsuario(value);
    }
    if (typeof onStep === 'function') {
      onStep(displayValue, isValid ? null : errorMsg);
    }
    if (current.key !== 'nome') {
      form.resetFields();
    }
  };

  return (
    <div key={step} className={`animate-slide-in-right ${styles.formContainer}`}>
      <div key={step} className={`animate-fade-in ${styles.interText}`}>{interTexts[step]}</div>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleNext}
        className={styles.form}
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
              className={styles.input}
            />
          </Form.Item>
        )}
        {current.type === 'number' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }} help={(
            <>
              {current.inputProps?.help && (
                <div className={styles.helpText}>
                  {current.inputProps.help}
                </div>
              )}
            </>
          )}>
            <Input
              type="number"
              size="large"
              {...current.inputProps}
              autoFocus
              placeholder={current.inputProps?.placeholder || 'Digite aqui...'}
              className={styles.input}
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
              className={styles.input}
              onChange={e => {
                const val = e.target.value.replace(/[^0-9.,]/g, '');
                form.setFieldsValue({ [current.key]: val });
              }}
              onBlur={e => {
                const val = e.target.value.replace(',', '.');
                form.setFieldsValue({ [current.key]: val });
              }}
            />
          </Form.Item>
        )}
        {current.type === 'select' && (
          <Form.Item name={current.key} label={false} rules={current.rules} style={{ marginBottom: 0 }}>
            <div className={styles.selectGroup}>
              {current.options.map(opt => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => {
                    form.setFieldsValue({ [current.key]: opt.value });
                    setTimeout(() => form.submit(), 100);
                  }}
                  className={
                    form.getFieldValue(current.key) === opt.value
                      ? `${styles.selectBtn} ${styles.selected}`
                      : styles.selectBtn
                  }
                  tabIndex={0}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </Form.Item>
        )}
        {current.type !== 'select' && <button type="submit" style={{ display: 'none' }} />}
      </Form>

      <div className={`animate-fade-in ${styles.instruction}`}>
        <span className={styles.instructionEnter}>Enter</span>
        para enviar
        <span className={styles.instructionIcon}>⚡</span>
      </div>
    </div>
  );
}
